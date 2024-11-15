
Generic tips

---



`# Filter the handlers_by_user dictionary to include only admin users
# admin_handlers = {user_id: handlers for user_id, handlers in global_handlers.items() if user_id in bot.admin_users}
                          
# user_handlers = {**user_handlers, 0: global_handlers[0]}
# exclude duplicate keys from user_handlers
# user_handlers = {k: v for k, v in user_handlers.items() if k not in admin_handlers} `


---
