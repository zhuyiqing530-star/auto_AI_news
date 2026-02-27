try:
    from plyer import notification

    def notify(title: str, message: str):
        notification.notify(
            title=title,
            message=message[:200],
            app_name="AI News Aggregator",
            timeout=10,
        )
except ImportError:
    def notify(title: str, message: str):
        print(f"[NOTIFY] {title}: {message}")
