import axios from 'axios';
import React from 'react';
import Plot from 'react-plotly.js';


export default class UserByGender extends React.Component {

  state = {
    stats: []
  }

  componentDidMount() {
    axios.get(`http://localhost:8090/pie?field=gender`)
      .then(res => {
        const stats = res.data.result.gender;
        this.setState({ stats });
      })
  }

  render() {
    if (this.state.stats) {
      const genders = Object.keys(this.state.stats)
      const counts = Object.values(this.state.stats)

      return (
        <div>
          <h2>Userbase by Gender</h2>
          <Plot
            data={
              [{
                values: counts,
                labels: genders,
                type: 'pie',
                hole: .4,
              }]
            }
            layout={
              {
                title: 'Pie Chart',
                height: 400,
                width: 800
              }
            }
          />
        </div>
      );
    } else {
      <p>Loading....</p>
    }
  }
}