import {ReactNode} from 'react'

import s from './button.module.css'

type ButtonProps = {
  children?: ReactNode
  disabled?: boolean
  onClick?: () => void
}

export const Button = ({children, onClick, disabled}: ButtonProps) => {
  return (
    <button onClick={onClick} className={s.btn} disabled={disabled}>
      {children}
    </button>
  )
}