import {connectQuery, createQuery} from "@farfetched/core";
import {query} from "../../shared/lib/query.ts";
import {registerQuery} from "../register/model.ts";
import {loginQuery} from "../login/model.ts";

export const initialQuery = createQuery({
  name: 'initialQuery',
  handler: async () => await query('common/initial', 'post')
})

export const updateUserQuery = createQuery({
  name: 'updateUserQuery',
  handler: async (payload) => await query('user/update', 'post', payload)
})

export const logoutQuery = createQuery({
  name: 'logoutQuery',
  handler: async () => await query('auth/logout', 'post')
})

connectQuery({
  source: registerQuery,
  target: initialQuery
})

connectQuery({
  source: logoutQuery,
  target: initialQuery
})

connectQuery({
  source: loginQuery,
  target: initialQuery
})

connectQuery({
  source: updateUserQuery,
  target: initialQuery
})