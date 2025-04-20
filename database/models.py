from tortoise import models, fields


class User(models.Model):
    tg_id = fields.CharField(max_length=10, unique=True)
    username = fields.CharField(max_length=32, null=True)
    name = fields.CharField(max_length=129)  # 128 max chars + spacebar
    is_active = fields.BooleanField(default=True)
    points = fields.IntField(default=3)

    def __str__(self):
        return f"{self.name} - {self.username} - {self.tg_id}"

    def save(self, *args, **kwargs):
        if self.points < 0:
            self.points = 0

        super().save(*args, **kwargs)


class Category(models.Model):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    content = fields.TextField()
    category = fields.ForeignKeyField("models.Category", on_delete=fields.SET_NULL, related_name="posts", null=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="posts")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]