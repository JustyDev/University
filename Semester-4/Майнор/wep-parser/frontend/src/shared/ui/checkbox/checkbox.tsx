import { ChangeEvent, forwardRef, useState } from 'react';
import s from './checkbox.module.css';

type CheckboxProps = {
  label?: string;
  checked: boolean;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  className?: string;
  disabled?: boolean;
  id?: string;
  name?: string;
};

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, checked, onChange, className, disabled, id, name }, ref) => {
    const [isFocused, setIsFocused] = useState(false);

    return (
      <label 
        className={`
          ${s.checkbox} 
          ${className || ''} 
          ${disabled ? s.disabled : ''}
          ${isFocused ? s.focused : ''}
        `}
      >
        <input
          ref={ref}
          type="checkbox"
          checked={checked}
          onChange={onChange}
          disabled={disabled}
          id={id}
          name={name}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
        />
        <span className={s.checkmark}>
          <svg viewBox="0 0 12 10">
            <path d="M1 5.5L4.5 9L11 1" stroke="currentColor" strokeWidth="2" fill="none" />
          </svg>
        </span>
        {label && <span className={s.label}>{label}</span>}
      </label>
    );
  }
);

Checkbox.displayName = 'Checkbox';
