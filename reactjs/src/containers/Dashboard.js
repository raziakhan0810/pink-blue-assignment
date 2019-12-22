import React from 'react';

class Dashboard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div className="container">
                <br />
                <div className="row heading">
                    <div className="col-lg-2 col-sm-4">
                    Welcome to Dashboard
                    </div>
                </div>
                <br/>
            </div>
        );
    }
}

export default Dashboard;

