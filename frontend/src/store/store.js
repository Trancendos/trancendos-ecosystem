/**
 * @fileoverview Redux store configuration.
 * @version 1.0.0
 * @author Trancendos
 */

import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import transactionReducer from './transactionSlice';

/**
 * The Redux store.
 * @type {object}
 */
export const store = configureStore({
  reducer: {
    auth: authReducer,
    transactions: transactionReducer,
  },
});