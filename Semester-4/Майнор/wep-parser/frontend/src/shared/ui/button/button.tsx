import {ButtonHTMLAttributes, ReactNode} from 'react';
import clsx from 'clsx';
import s from './button.module.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'icon';
  size?: 'small' | 'medium' | 'large';
}

export const Button = ({
                         children,
                         variant = 'secondary',
                         size = 'medium',
                         className = '',
                         ...props
                       }: ButtonProps) => {
  return (
    <button
      className={clsx(
        s.button,
        s[variant],
        s[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};
