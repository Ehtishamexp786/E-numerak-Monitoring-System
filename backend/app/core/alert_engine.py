import httpx
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.monitor import Monitor, MonitorStatus
from app.models.alert import Alert, AlertType, AlertStatus
from app.config import settings


async def send_whatsapp_alert(phone_number: str, message: str) -> bool:
    try:
        url = f"{settings.GREEN_API_URL}/waInstance{settings.GREEN_API_INSTANCE_ID}/sendMessage/{settings.GREEN_API_TOKEN}"

        payload = {
            "chatId": f"{phone_number}@c.us",
            "message": message
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)

            if response.status_code == 200:
                print(f"✅ WhatsApp Alert Send: {phone_number}")
                return True
            else:
                print(f"❌ WhatsApp alert fail: {response.text}")
                return False

    except Exception as e:
        print(f"❌ WhatsApp error: {str(e)}")
        return False


async def process_alerts(check_result: dict, monitor: Monitor, db: AsyncSession):
    # Sirf tab alert karo jab status change hua ho
    if check_result["old_status"] == check_result["new_status"]:
        return

    if not monitor.alert_on_down:
        return

    if not monitor.alert_whatsapp_numbers:
        return

    # Alert message banao
    if check_result["new_status"] == MonitorStatus.DOWN:
        alert_type = AlertType.DOWN
        emoji = "🔴"
        message = f"""
{emoji} *SERVER DOWN ALERT!*

📌 Monitor: {monitor.name}
🌐 URL: {monitor.url}
❌ Status: DOWN
⏱ Response Time: {check_result['response_time_ms']:.0f}ms
❗ Error: {check_result['error_message']}
🕐 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

Foran check karo!
        """.strip()

    elif check_result["new_status"] == MonitorStatus.UP:
        alert_type = AlertType.UP
        emoji = "🟢"
        message = f"""
{emoji} *SERVER BACK ONLINE!*

📌 Monitor: {monitor.name}
🌐 URL: {monitor.url}
✅ Status: UP
⏱ Response Time: {check_result['response_time_ms']:.0f}ms
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

Server wapas chal gaya!
        """.strip()
    else:
        return

    # Har number ko alert bhejo
    numbers = [n.strip() for n in monitor.alert_whatsapp_numbers.split(",")]

    for number in numbers:
        if not number:
            continue

        success = await send_whatsapp_alert(number, message)

        # Alert record save karo
        alert = Alert(
            monitor_id=monitor.id,
            monitor_name=monitor.name,
            alert_type=alert_type,
            status=AlertStatus.SENT if success else AlertStatus.FAILED,
            message=message,
            whatsapp_number=number,
            sent_at=datetime.now() if success else None
        )
        db.add(alert)

    await db.commit()