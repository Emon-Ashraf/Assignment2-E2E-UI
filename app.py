from flask import Flask, request, render_template
from solution import Solution

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_courses = int(request.form['num_courses'])
            prerequisites = eval(request.form['prerequisites'])  # Convert the input string to a list of lists
            solution = Solution()
            course_order = solution.findOrder(num_courses, prerequisites)
        except (SyntaxError, NameError):
            return render_template('index.html', course_order='Invalid prerequisites format')
        except ValueError:
            return render_template('index.html', course_order='Invalid number format')
        except Exception as e:
            return render_template('index.html', course_order=f'Error: {str(e)}')

        return render_template('index.html', course_order=course_order)
    return render_template('index.html', course_order=None)


if __name__ == '__main__':
    app.run(debug=True)
