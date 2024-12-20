import {createQuery} from "@farfetched/core";
import {query} from "../../shared/lib/query.ts";

export const registerQuery = createQuery({
  name: 'registerQuery',
  handler: async payload => await query('auth/register', 'post', payload)
})