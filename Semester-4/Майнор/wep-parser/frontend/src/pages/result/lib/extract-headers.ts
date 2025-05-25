import {ParseResultDto} from "@shared/api";

export const extractHeaders = (data: ParseResultDto['results'][0]['data']) => {
  const headers: {
    level: number,
    text: string
  }[] = []

  data?.h1?.forEach(header => {
    headers.push({
      level: 1,
      text: header
    })
  })

  data?.h2?.forEach(header => {
    headers.push({
      level: 2,
      text: header
    })
  })

  data?.h3?.forEach(header => {
    headers.push({
      level: 3,
      text: header
    })
  })

  data?.h4?.forEach(header => {
    headers.push({
      level: 4,
      text: header
    })
  })

  data?.h5?.forEach(header => {
    headers.push({
      level: 5,
      text: header
    })
  })

  data?.h6?.forEach(header => {
    headers.push({
      level: 6,
      text: header
    })
  })

  return headers
}