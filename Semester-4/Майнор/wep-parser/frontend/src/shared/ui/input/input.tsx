import { InputHTMLAttributes } from 'react';
import styles from './input.module.css';

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  size?: 'small' | 'medium' | 'large';
}

export const Input = ({ 
  size = 'medium', 
  className = '', 
  ...props 
}: InputProps) => {
  return (
    <input 
      className={`${styles.input} ${styles[size]} ${className}`}
      {...props}
    />
  );
};
