class TimelineAnalysis:
    def monthly_timeline(self, selected_user,df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

        timeline['time'] = time

        return timeline

    def daily_timeline(self, selected_user,df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        daily_timeline = df.groupby('date').count()['message'].reset_index()

        return daily_timeline