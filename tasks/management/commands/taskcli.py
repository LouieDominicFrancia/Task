from django.core.management.base import BaseCommand
from tasks.models import Task
from datetime import datetime

class Command(BaseCommand):
    help = 'Command-Line Task Manager'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("📋 Welcome to the Task Manager CLI!\n"))
        
        while True:
            self.stdout.write("Choose an option:")
            self.stdout.write("1. List tasks")
            self.stdout.write("2. Add task")
            self.stdout.write("3. Update task status")
            self.stdout.write("4. Delete task")
            self.stdout.write("5. Exit")
            
            choice = input("Enter option (1-5): ").strip()

            if choice == '1':
                self.list_tasks()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.update_task_status()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.stdout.write("👋 Goodbye!")
                break
            else:
                self.stdout.write(self.style.WARNING("❌ Invalid choice. Try again.\n"))

    def list_tasks(self):
        tasks = Task.objects.all()
        if not tasks:
            self.stdout.write("No tasks found.\n")
        for task in tasks:
            self.stdout.write(
                f"[{task.id}] {task.title} | Status: {task.status} | Priority: {task.priority} | Due: {task.due_date}"
            )

    def add_task(self):
        title = input("Title: ")
        description = input("Description: ")
        priority = input("Priority (Low/Medium/High): ").capitalize()
        due = input("Due date (YYYY-MM-DD): ")

        try:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
            task = Task.objects.create(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                status='Pending'
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Task '{task.title}' added successfully!\n"))
        except ValueError:
            self.stdout.write(self.style.ERROR("❌ Invalid due date format.\n"))

    def update_task_status(self):
        try:
            task_id = int(input("Enter Task ID: "))
            task = Task.objects.get(pk=task_id)
            new_status = input("Enter new status (Pending/Completed): ").capitalize()
            if new_status in ['Pending', 'Completed']:
                task.status = new_status
                task.save()
                self.stdout.write(self.style.SUCCESS("✅ Status updated.\n"))
            else:
                self.stdout.write(self.style.ERROR("❌ Invalid status.\n"))
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Task not found.\n"))
        except ValueError:
            self.stdout.write(self.style.ERROR("❌ Invalid input. Must be a number.\n"))

    def delete_task(self):
        try:
            task_id = int(input("Enter Task ID to delete: "))
            task = Task.objects.get(pk=task_id)
            confirm = input(f"Are you sure you want to delete '{task.title}'? (y/n): ").lower()
            if confirm == 'y':
                task.delete()
                self.stdout.write(self.style.SUCCESS("🗑️ Task deleted.\n"))
            else:
                self.stdout.write("❎ Deletion cancelled.\n")
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Task not found.\n"))
        except ValueError:
            self.stdout.write(self.style.ERROR("❌ Invalid input.\n"))
