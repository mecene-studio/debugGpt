import React from 'react';
import s from './Button.module.scss';

interface ButtonProps {
  onClick: () => void;
  text: string;
}

const Button: React.FC<ButtonProps> = ({ onClick, text }) => {
  return (
    <button className={s.button} onClick={onClick}>
      {text}
    </button>
  );
};

export default Button;
