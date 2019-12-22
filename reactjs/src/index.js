// import React from 'react';
// import ReactDOM from 'react-dom';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import './index.sass';
// import App from './App';
// import registerServiceWorker from './registerServiceWorker';
//
// ReactDOM.render(<App />, document.getElementById('root'));
// registerServiceWorker();


import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Dashboard from './containers/Dashboard';
import App from './App';
import './index.sass';
import 'bootstrap/dist/css/bootstrap.min.css';

render(
        <div>
            <Router>
                <div>
                    <Route exact path="/" component={App}/>
                    <Route path="/dashboard" component={Dashboard}/>
                </div>
            </Router>
        </div>,
    document.getElementById('root')
);