from examPaperResults import examPaperResults

# Creating an instance of the examPaperResults class
results = examPaperResults()


def lessons_of_the_incorrect_questions():
    listOfLessons = []
    # Retrieving the questions which student answered incorrectly
    incorrect_questions = results.incorrect_questions()

    # Filtering out the lessons of the questions which student answered incorrectly
    for i in incorrect_questions:
        for key,value in i.items():
            if key == "RelatedLesson":
                listOfLessons.append(value)

    return listOfLessons

print(lessons_of_the_incorrect_questions())


