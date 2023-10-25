import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Post, User, Comment


class Command(BaseCommand):
    help = 'Generate 20 random cat-related posts'

    def handle(self, *args, **kwargs):
        user = User.objects.first()  # Assuming you have at least one user in your database

        if not user:
            self.stdout.write(self.style.ERROR(
                'No users found. Please create a user first.'))
            return

        titles = [
            "The Mystery of Cats",
            "Top 10 Cat Breeds",
            "How to Train Your Cat",
            "Understanding Cat Behavior",
            # ... add more titles
        ]

        for i in range(20):
            title = random.choice(titles)
            slug = f"{title.lower().replace(' ', '-')}-{i}"
            body = f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. {title}..."

            post = Post(
                title=title,
                slug=slug,
                author=user,
                body=body,
                publish=timezone.now(),
                status=Post.Status.PUBLISHED
            )
            post.save()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created post {post.title}'))
