from dataclasses import dataclass


@dataclass(order=True)
class BreakInterval:
    begin: int
    end: int

    @staticmethod
    def get_time(sec):
        hours = str(sec // BreakTemplateParser.HOUR_TO_SECONDS)
        rest = sec % BreakTemplateParser.HOUR_TO_SECONDS
        minutes = str(rest // BreakTemplateParser.MINUTE_TO_SECONDS)
        seconds = str(sec % BreakTemplateParser.MINUTE_TO_SECONDS)
        return f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}"

    def __repr__(self):
        return f"Break({self.get_time(self.begin)}, {self.get_time(self.end)})"


class BreakTemplateParser:
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60

    @staticmethod
    def is_valid_interval(interval, class_start_in_seconds, class_end_in_seconds):
        return interval.begin > class_start_in_seconds and interval.end < class_end_in_seconds

    @classmethod
    def convert_time_to_seconds(cls, time):
        split_time = time.split(':')
        return int(split_time[0]) * cls.HOUR_TO_SECONDS + \
            int(split_time[1]) * cls.MINUTE_TO_SECONDS + int(split_time[2])

    def __init__(self, template_json, class_begin_time, class_end_time):
        self.class_start_in_seconds = self.convert_time_to_seconds(class_begin_time)
        self.class_end_in_seconds = self.convert_time_to_seconds(class_end_time)
        self.is_relative_to_start = True if template_json["start_time_type"] == "RELATIVE_TO_CLASS_START" else False
        self.start_times = template_json["start_times"]
        self.duration = template_json["break_duration"]

    def construct_valid_interval_list(self):
        intervals = []
        for break_start_time in self.start_times:
            break_start_in_seconds = self.convert_time_to_seconds(break_start_time)
            if self.is_relative_to_start:
                interval = BreakInterval(self.class_start_in_seconds + break_start_in_seconds,
                                         self.class_start_in_seconds + break_start_in_seconds + self.duration * self.MINUTE_TO_SECONDS)
            else:
                interval = BreakInterval(self.class_end_in_seconds - break_start_in_seconds,
                                         self.class_end_in_seconds - break_start_in_seconds + self.duration * self.MINUTE_TO_SECONDS)
            if self.is_valid_interval(interval, self.class_start_in_seconds, self.class_end_in_seconds):
                intervals.append(interval)
        return intervals
