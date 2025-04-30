import re
import pandas as pd
from datetime import datetime


class Preprocessor:
    def __init__(self):
        self.patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[APap][Mm]))\s-\s([^:]+):\s(.+)',  # old dash format
            r'\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?::\d{2})?\s?[APap][Mm])\]\s([^:]+):\s(.+)'  # new bracket format
        ]

    def preprocess(self, file_contents):
        chat_data = file_contents.splitlines()
        messages = []

        for line in chat_data:
            for pattern in self.patterns:
                match = re.match(pattern, line)
                if match:
                    date_str, time_str, sender, message = match.groups()
                    full_datetime = f"{date_str}, {time_str}".replace("\u202f", " ").replace(" ", " ")
                    messages.append([full_datetime, date_str, sender.strip(), message.strip()])
                    break  # once matched, skip checking other patterns

        df = pd.DataFrame(messages, columns=["user_message", "date", "user", "message"])

        # Handle date column
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

        df["year"] = df["date"].dt.year
        df["month_num"] = df["date"].dt.month
        df["month"] = df["date"].dt.strftime("%B")
        df["day"] = df["date"].dt.day
        df["day_name"] = df["date"].dt.strftime("%A")

        # Time extraction with fallback
        df["hour"] = pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M %p", errors="coerce").dt.hour.fillna(
            pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M:%S %p", errors="coerce").dt.hour
        )

        df["minute"] = pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M %p", errors="coerce").dt.minute.fillna(
            pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M:%S %p", errors="coerce").dt.minute
        )

        period = []
        for hour in df["hour"].fillna(0).astype(int):
            if hour == 23:
                period.append(f"{hour}-00")
            elif hour == 0:
                period.append("00-1")
            else:
                period.append(f"{hour}-{hour + 1}")
        df["period"] = period

        return df[["user_message", "date", "user", "message", "year", "month_num", "month", "day", "day_name", "hour", "minute", "period"]]
