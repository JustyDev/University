import {createQuery} from "@farfetched/core";
import {query} from "../../shared/lib/query.ts";

export const loginQuery = createQuery({
  name: 'loginQuery',
  handler: async (payload) => await query('auth/login', 'post', payload)
})