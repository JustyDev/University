import s from './input.module.css'
import { HTMLInputTypeAttribute } from 'react'

type InputProps = {
  placeholder?: string;
  value?: string;
  type?: HTMLInputTypeAttribute;
  onUpdate?: (val: string) => void;
}

export const Input = (props: InputProps) => {

  const { placeholder, value, onUpdate, type = 'text' } = props

  return (
    <input
      type={type}
      onChange={e => {
        onUpdate?.(e.target.value)
      }}
      value={value}
      className={s.inp}
      placeholder={placeholder}
    />
  )
}