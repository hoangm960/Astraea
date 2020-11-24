import pickle


def load_assignments(filename):
    with open(filename, "rb") as f:
        unpickler = pickle.Unpickler(f)
        data = unpickler.load()
        assignments = data[1]
        cls_assignments = {}
        for assignment in assignments:
            cls_assignments[assignment.name] = assignment.details
        print(cls_assignments)

load_assignments("data/Lesson/assignments.list")
