import s from './input.module.css'
import {HTMLInputTypeAttribute} from 'react'

type InputProps = {
  placeholder?: string;
  value?: string;
  disabled?: boolean;
  type?: HTMLInputTypeAttribute;
  onUpdate?: (val: string) => void;
}

export const Input = (props: InputProps) => {

  const {placeholder, value, onUpdate, type = 'text', disabled} = props

  return (
    <input
      disabled={disabled}
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