const initialState = {
    // todo : Validate token first. If token not valid, treat user as not logged in

    email: localStorage.getItem('email') ? localStorage.getItem('email') : null,
    username: localStorage.getItem('username') ? localStorage.getItem('username') : null,
    password: localStorage.getItem('password') ? localStorage.getItem('password') : null,
    isLoggedIn: !!localStorage.getItem('token'),
    loginError: null,
    token: localStorage.getItem('token') ? localStorage.getItem('token') : null,
};

function user(state = initialState, action) {
    let newState = Object.assign({}, state);
    switch (action.type) {

        case 'LOGIN_SUCCESSFUL':
            newState.email = action.response.email;  //
            newState.username = action.response.username;  //
            newState.password = action.response.password;  //
            newState.token = action.response.token;  //
            newState.isLoggedIn = true;  //

            localStorage.setItem('isLoggedIn', newState.isLoggedIn);
            localStorage.setItem('email', newState.email);
            localStorage.setItem('username', newState.username);
            localStorage.setItem('password', newState.password);
            localStorage.setItem('token', newState.token);

            return newState;

        default:
            return state;
    }
}

export default user;