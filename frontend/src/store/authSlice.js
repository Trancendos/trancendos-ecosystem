/**
 * @fileoverview Redux slice for authentication state management.
 * @version 1.0.0
 * @author Trancendos
 */

import { createSlice } from '@reduxjs/toolkit';

/**
 * The initial state for the authentication slice.
 * @type {object}
 */
const initialState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,
};

/**
 * The Redux slice for authentication.
 */
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    /**
     * Sets the loading state to true and clears any previous errors.
     * @param {object} state - The current state.
     */
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    /**
     * Sets the user and token upon successful login.
     * @param {object} state - The current state.
     * @param {object} action - The Redux action.
     */
    loginSuccess: (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    /**
     * Sets the error message upon login failure.
     * @param {object} state - The current state.
     * @param {object} action - The Redux action.
     */
    loginFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    /**
     * Clears the user, token, and authentication status upon logout.
     * @param {object} state - The current state.
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