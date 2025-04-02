class ActivityMap:
    def week_activity_map(self , selected_user,df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        return df['day_name'].value_counts()

    def month_activity_map(self,selected_user,df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        return df['month'].value_counts()

    def activity_heatmap(self, selected_user,df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

        return user_heatmap
