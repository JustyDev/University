import {useUnit} from "effector-react";
import {Query} from "@farfetched/core";
import {ApiError} from "../lib/query.ts";

export const useQueryError = (err: Query<any, any, any, any>) => {

  const {error} = useUnit(err)

  let message: string | undefined
  let attachments: object | undefined
  let code: number | undefined
  let type: string | undefined
  let isError: boolean = false

  if (error && error instanceof ApiError) {
    message = error.message
    attachments = error.attachments
    code = error.code
    type = error.type
  }

  if (message) isError = true

  return {
    message: message,
    attachments: attachments,
    code: code,
    type: type,
    isError: isError
  }
}