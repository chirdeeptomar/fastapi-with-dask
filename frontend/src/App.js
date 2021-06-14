import React from 'react';
import './App.css';
import UserByCountry from './components/UserByCountry';
import UserByGender from './components/UserByGender';
import UserBySalary from './components/UserBySalary';

export default class App extends React.Component {

  render() {
    return (
      <div>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
          <UserByCountry />
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
          <UserByGender />
          <UserBySalary />
        </div>
      </div >
    )
  }
}