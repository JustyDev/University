import { ReactNode } from 'react'

import s from './button.module.css'

type ButtonProps = {
  children?: ReactNode
}

export const Button = ({ children }: ButtonProps) => {
  return (
    <button className={s.btn}>
      {children}
    </button>
  )
}