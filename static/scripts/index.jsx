import React from 'react';
import ReactDOM from 'react-dom';

const tableStyle = {
  width: '80%'
};

class MarksList extends React.Component {

    constructor(props) {
      super(props);
      this.state = {marks: {}, studentlist: []};
    }

    getStudents() {
      $.ajax({
        url: '/students',
        dataType: 'json',
        cache: false,
        success: function(studentlist) {
          this.setState( { studentlist:  studentlist });
          studentlist.forEach(function(student) {
            this.getMark(student.key);
          }.bind(this));
        }.bind(this),
        error: function(xhr, status, err) {
          console.error(status, err.toString());
        }.bind(this)
      });
    }

    getMark(key) {
      console.log('key:' + key);
      $.ajax({
        url: '/getmark/' + key,
         dataType: 'json',
         cache: false,
         success: function(mark) {
           mark.tests_correct.sort();
           var marks = this.state.marks;
           marks[key] = {total: mark.total, correct: mark.tests_correct.join()};
           this.setState({marks: marks});
         }.bind(this),
         error: function(xhr, status, err) {
           console.error(status, err.toString());
         }.bind(this)
      });
    }

    getInfo() {
      this.getStudents();

    }

    componentDidMount() {
      this.getInfo();
    }

    render() {
      var rows = [];
      if (this.state && this.state.studentlist)
        this.state.studentlist.forEach(function(student) {
          var key = student.key;
          var mark = 0;
          var tests_correct = '';
          if (this.state.marks && key in this.state.marks) {
            mark = this.state.marks[key].total;
            tests_correct = this.state.marks[key].correct;
          }
          var notebook_link = '/student_notebook/' + student.key;
          var notebook_filename = student.email + '.ipynb';
          rows.push(<tr>
            <td>{student.email}</td>
            <td>{mark}</td>
            <td>{tests_correct}</td>
            <td><a href={notebook_link} download={notebook_filename}>Notebook</a></td>
            </tr>);
        }.bind(this));

      return(
        <div className="table-responsive">
          <table className="table-bordered" style={tableStyle}>
            <tr>
              <th>Email</th>
              <th>Mark</th>
              <th>Tests Correct</th>
              <th>Download notebook</th>
            </tr>
            {rows}
          </table>
        </div>
      );
    }
}

ReactDOM.render(
  <MarksList />,
  document.getElementById('indexdiv')
);
