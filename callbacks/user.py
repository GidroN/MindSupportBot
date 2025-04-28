from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from constants.callbacks import CallbackConstants
from constants.factory import PaginationMarkup, DeletePostAction, PostChangeItem, SearchPostType
from database.models import Category, Post, User
from keyboards.builders import post_kb, categories
from keyboards.factories import ChooseCategoryCallback, PaginationCallback, MessageUserCallback, \
    DeletePostCallback, ChangePostInfoCallback
from keyboards.inline import confirm_post_delete_kb
from keyboards.reply import cancel_button_kb, profile_user_kb
from misc.states import SearchPostForm, AddPostForm, MessageUserForm, DeletePostForm, EditPostForm
from misc.utils import send_user_post_info, send_user_change_post_info

router = Router(name="user_callbacks")


@router.callback_query(AddPostForm.category, ChooseCategoryCallback.filter())
async def choose_category_to_add_post(callback: CallbackQuery, callback_data: ChooseCategoryCallback, state: FSMContext):
    category_id = callback_data.category_id
    category = await Category.get(id=category_id)

    await state.set_state(AddPostForm.enter_text)
    await state.update_data(category_id=category_id)

    await callback.answer(f"Вы перешли в категорию {category.name}")
    await callback.message.answer(f"Отлично. Теперь пришлите пост", reply_markup=cancel_button_kb)


@router.callback_query(SearchPostForm.category, ChooseCategoryCallback.filter())
async def choose_category_to_search_post(callback: CallbackQuery, callback_data: ChooseCategoryCallback, state: FSMContext):
    category_id = callback_data.category_id
    category = await Category.get_or_none(id=category_id)

    if callback_data.search_type == SearchPostType.ALL_POSTS:
        posts_list = await Post.all().prefetch_related("category", "user")
        posts_list_ids = await Post.all().values_list("id", flat=True)
        await callback.answer(f"Вы перешли к просмотру всех постов")

    else: # callback_data.search_type == SearchPostType.BY_CATEGORY
        if await Post.filter(category=category).count() == 0:
            await callback.answer("В данной категории пока что нет постов.", show_alert=True)
            return

        await callback.answer(f"Вы перешли в категорию {category.name}")
        await state.update_data(category_id=category_id)

        posts_list = await Post.filter(category=category).prefetch_related("user", "category")
        posts_list_ids = await Post.filter(category=category).values_list("id", flat=True)

    await send_user_post_info(posts_list=posts_list, callback=callback)
    await state.set_state()
    await state.update_data(post_list_ids=posts_list_ids)


@router.callback_query(default_state, PaginationCallback.filter())
async def process_search_result(callback: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):

    data = await state.get_data()
    ids = data["post_list_ids"]
    result = await Post.filter(id__in=ids).prefetch_related("user", "category")

    page = callback_data.page
    action = callback_data.action

    if action == "next":
        page += 1
    elif action == "prev":
        page -= 1

    if page < 0:
        page = 0
        await callback.answer("Это первая запись.")
        return
    elif page >= len(result):
        page = len(result) - 1
        await callback.answer("Это последняя запись.")
        return

    if callback_data.markup == PaginationMarkup.VIEWER:
        await send_user_post_info(result, callback, page=page)
    else: # callback_data.makup == PaginationMarkup.OWNER
        await send_user_change_post_info(result, callback.message, page=page, edit_msg=True)

    await callback.answer()


@router.callback_query(default_state, MessageUserCallback.filter())
async def message_user_callback(callback: CallbackQuery, callback_data: MessageUserCallback, state: FSMContext):
    to_user = callback_data.to_user
    from_user = callback_data.from_user
    post_id = callback_data.post_id
    reply_to_message_id = callback_data.reply_to_message_id

    await callback.answer("Вы отправляете сообщение автору")
    await callback.message.answer("Наберите сообщение, которое хотите отправить автору.", reply_markup=cancel_button_kb)
    await state.set_state(MessageUserForm.enter_message)
    await state.update_data(to_user=to_user, post_id=post_id, from_user=from_user, reply_to_message_id=reply_to_message_id)


@router.callback_query(default_state, ChangePostInfoCallback.filter())
async def change_post_info(callback: CallbackQuery, callback_data: ChangePostInfoCallback, state: FSMContext):
    await callback.answer()

    change_item = callback_data.change_item
    post_id = callback_data.post_id

    if change_item == PostChangeItem.CATEGORY:
        await callback.message.answer("Выберите категорию",
                                      reply_markup=await categories(cancel=True, show_number_items=False))
        await state.set_state(EditPostForm.category)

    else: # delete
        await callback.message.answer("Вы уверены, что хотите удалить этот пост?", reply_markup=confirm_post_delete_kb)
        await state.set_state(DeletePostForm.confirm)
        await state.update_data(post_id=post_id, message_id=callback.message.message_id)

    await state.update_data(change_item=change_item, post_id=post_id)

@router.callback_query(DeletePostForm.confirm, DeletePostCallback.filter())
async def delete_post(callback: CallbackQuery, callback_data: DeletePostCallback, state: FSMContext):
    action = callback_data.action
    data = await state.get_data()
    post_id = data["post_id"]
    message_to_delete = data["message_id"]
    post_list_ids = data["post_list_ids"]
    post = await Post.get(id=post_id)

    if action == DeletePostAction.CANCEL:
        await callback.answer("Отменено.")
        await callback.message.delete()
    else:  # action == CONFIRM
        await post.delete()
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=message_to_delete,
        )
        await callback.message.delete()
        await callback.answer("Пост успешно удален!")

        post_list_ids.remove(post_id)

        posts = await Post.filter(id__in=post_list_ids).prefetch_related("user", "category")
        post_list_ids = await Post.filter(id__in=post_list_ids).values_list("id", flat=True)

        if posts:
            await send_user_change_post_info(posts, callback.message)
            await state.update_data(post_list_ids=post_list_ids)
        else:
            await callback.message.answer("Больше постов не осталось.", reply_markup=profile_user_kb)


    await state.set_state()


@router.callback_query(EditPostForm.category, ChooseCategoryCallback.filter())
async def change_category_message(callback: CallbackQuery, callback_data: ChooseCategoryCallback, state: FSMContext):
    data = await state.get_data()
    post_id = data["post_id"]
    category_id = callback_data.category_id

    category = await Category.get(id=category_id)
    post = await Post.get(id=post_id)

    post.category = category
    await post.save()

    await callback.answer("Категория успешно изменена")
    await callback.message.delete()

    await state.set_state()


@router.callback_query(EditPostForm.category, F.data == CallbackConstants.DELETE_CATEGORY_MESSAGE)
async def remove_category_change_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state()
