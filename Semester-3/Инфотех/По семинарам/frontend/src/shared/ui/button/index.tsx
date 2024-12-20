import {ReactNode} from 'react'

import s from './button.module.css'

type ButtonProps = {
  children?: ReactNode
  onClick?: () => void
}

export const Button = ({children, onClick}: ButtonProps) => {
  return (
    <button onClick={onClick} className={s.btn}>
      {children}
    </button>
  )
}