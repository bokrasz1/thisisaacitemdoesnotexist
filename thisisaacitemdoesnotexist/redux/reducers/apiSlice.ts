import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query";

export const apiSlice = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({baseUrl: 'http://127.0.0.1:8000'}),
    endpoints: (builder) => ({
        getTest: builder.query<string,void>({
            query: () => `/api/test`,
        })
    }),
})