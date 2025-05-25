import {useEffect, useState} from 'react';
import s from './main-background.module.css';

const Dot = ({row, col}: { row: number; col: number }) => {
  const [isActive, setIsActive] = useState(false);

  const activationProbability = 100 / 100;

  useEffect(() => {
    const checkActivation = () => {
      if (Math.random() * 100 < activationProbability) {
        setIsActive(true);

        setTimeout(() => setIsActive(false), 1000);
      }
      // Check again in 100-300ms
      setTimeout(checkActivation, 100 + Math.random() * 200);
    };

    const timeout = setTimeout(checkActivation, (row + col) * 20);
    return () => clearTimeout(timeout);
  }, [row, col, activationProbability]);

  return (
    <div
      className={`${s.dot} ${isActive ? s.active : ''}`}
      style={{
        animationDelay: `${(col + row) * 70}ms`,
        left: `${col * 80}px`,
        top: `${row * 80}px`
      }}
    />
  );
};

export const MainBackground = () => {
  const dots = [];
  for (let row = 0; row < 17; row++) {
    for (let col = 0; col < 25; col++) {
      dots.push(<Dot key={`${row}-${col}`} row={row} col={col}/>);
    }
  }

  return <div className={s.container}>{dots}</div>;
};
