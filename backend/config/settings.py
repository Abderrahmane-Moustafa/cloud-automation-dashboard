##config/settings.py
## هنا بنقرأ مفاتيح السر من .env علشان نحافظ عليها برا الكود.

from dotenv import load_dotenv
import os

load_dotenv()

AWS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET_KEY")

"""🔹 .env
ملف سري مش بيتحط في GitHub. بتحط فيه مفاتيح زي:"""