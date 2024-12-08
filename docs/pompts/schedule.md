

Looking at the current implementation, while it has a robust foundation, it doesn't yet have a dedicated task scheduling system. Let's add a new module to handle scheduled tasks with features like:

1. Task scheduling with cron-like expressions
2. Persistent task storage
3. Task management commands
4. Support for both one-time and recurring tasks

Implement Task Scheduler System

* Update

  `requirements.txt`

* Create

  `src/framework/task_scheduler.py`

* Update

  `src/framework/base.py`

I've added a comprehensive task scheduling system with the following features:

1. **Task Scheduler Class** :

* Supports different types of triggers (date, interval, cron)
* Persistent storage of tasks
* Task metadata management
* Task restoration on bot restart

1. **Integration with Framework** :

* Added TaskScheduler to the main framework
* Automatic task restoration when bot starts
* Proper initialization and shutdown

1. **Task Management Features** :

* Add tasks with various scheduling options
* Remove tasks
* List tasks (all or by user)
* Get task details
* Task persistence across bot restarts

To use the task scheduler, you can now create tasks like this:

```
# Add a daily task
await bot.task_scheduler.add_task(
    task_id="daily_backup",
    func=backup_function,
    trigger="cron",
    trigger_args={"hour": "0", "minute": "0"},
    name="Daily Backup",
    description="Performs daily backup at midnight",
    user_id=admin_id
)

# Add a one-time task
await bot.task_scheduler.add_task(
    task_id="reminder",
    func=reminder_function,
    trigger="date",
    trigger_args={"run_date": "2024-01-01 00:00:00"},
    name="New Year Reminder",
    description="Send New Year message",
    user_id=user_id
)
```

Would you like me to add command handlers for managing tasks through Telegram commands as well?
