import axios from 'axios';
import React from 'react';
import Plot from 'react-plotly.js';


export default class UserBySalary extends React.Component {

    state = {
        stats: []
    }

    componentDidMount() {
        axios.get(`http://localhost:8090/salary-distribution`)
            .then(res => {
                const stats = res.data.result.grouped_salary;
                this.setState({ stats });
            })
    }

    render() {
        if (this.state.stats) {
            const salaries = Object.keys(this.state.stats)
            const counts = Object.values(this.state.stats)

            return (
                <div style={{ paddingLeft: '100px' }}>
                    <h2>Userbase by Salary</h2>
                    <Plot
                        data={
                            [{
                                y: counts,
                                x: salaries,
                                type: 'scatter'
                            }]
                        }
                        layout={{
                            title: 'Scatter Plot',
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