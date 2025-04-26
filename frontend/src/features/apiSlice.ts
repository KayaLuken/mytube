import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api/' }), // Adjust base URL as needed
  endpoints: (builder) => ({
  }),
});

export const {  } = apiSlice; // Export hooks for components