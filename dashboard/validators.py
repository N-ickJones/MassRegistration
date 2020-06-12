from datetime import timedelta
import datetime


class DateAcceptableValidator:
    """
    validator to check that date submitted falls into an acceptable range after pre register limit and before close
    register limit
    """
    def __call__(self, mass):
        pre_register_days = mass.parish.pre_register
        pre_register_days = timedelta(days=pre_register_days)
        close_register_days = mass.parish.close_register
        close_register_days = timedelta(days=close_register_days)
        now = datetime.datetime.now()
        pre_register_date = mass.start - pre_register_days
        close_register_date = mass.start - close_register_days
        if pre_register_date < now < close_register_date:
            return True
        else:
            return False
