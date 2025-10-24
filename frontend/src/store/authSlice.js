import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,
};

/**
 * Redux slice for authentication management.
 */
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    /**
     * Sets the state to indicate that a login attempt is in progress.
     */
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    /**
     * Sets the state to indicate that a login attempt was successful.
     * @param {object} state - The current state.
     * @param {object} action - The action object containing the user and token.
     */
    loginSuccess: (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    /**
     * Sets the state to indicate that a login attempt failed.
     * @param {object} state - The current state.
     * @param {object} action - The action object containing the error message.
     */
    loginFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    /**
     * Logs the user out.
     */
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      localStorage.removeItem('token');
    },
  },
});

export const { loginStart, loginSuccess, loginFailure, logout } = authSlice.actions;
export default authSlice.reducer;