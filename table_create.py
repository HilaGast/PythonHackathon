class Table:

    def __init__(self,subject_data):
        self.subject_data=subject_data
    def frame_to_list(self):
        temp = []
        for row in self.subject_data.iterrows():
            index, data = row
            temp.append(data.tolist())
        return (temp)