import axios from 'axios';
import React from 'react';
import Plot from 'react-plotly.js';
import './App.css';


export default class App extends React.Component {

  state = {
    stats: []
  }

  componentDidMount() {
    axios.get(`http://localhost:8090/pie`)
      .then(res => {
        const stats = res.data.result.country;
        this.setState({ stats });
      })
  }

  render() {
    if (this.state.stats) {
      const countries = Object.keys(this.state.stats)
      const counts = Object.values(this.state.stats)

      return (
        <div>
          <Plot
            data={
              [{
                y: counts,
                x: countries,
                type: 'scatter'
              }]
            }
            layout={{
              title: 'Scatter Plot',
              height: 400,
              width: 800
            }}
          />
          <Plot
            data={
              [{
                values: counts,
                labels: countries,
                type: 'pie'
              }]
            }
            layout={{
              title: 'Pie Chart',
              height: 400,
              width: 800
            }}
          />
        </div>
      );
    } else {
      <p>Loading....</p>
    }
  }
}