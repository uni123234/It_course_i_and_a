import React, { useState, useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  width?: string;
  height?: string;
  children: React.ReactNode;
}

const ModalBase: React.FC<ModalProps> = ({ isOpen, onClose, width = '80%', height = '80vh', children }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      const timeout = setTimeout(() => setIsVisible(false), 300); // Таймаут для плавної анімації
      return () => clearTimeout(timeout);
    }
  }, [isOpen]);

  const closeModal = () => {
    setIsVisible(false);
    setTimeout(() => onClose(), 300); // Плавне закриття
  };

  if (!isOpen && !isVisible) return null;

  return (
    <>
      {/* Тло для затемнення */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300 backdrop-blur-sm z-10 ${
          isVisible ? 'opacity-100' : 'opacity-0'
        }`}
        onClick={closeModal}
      ></div>

      {/* Модальне вікно */}
      <div className="fixed inset-0 flex items-center justify-center z-50">
        <div
          style={{ width, height }}
          className={`bg-white p-4 rounded-2xl shadow-lg overflow-y-auto transition-transform transform duration-500 ${
            isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'
          }`}
        >
          <button onClick={closeModal} className="absolute top-4 right-4 text-gray-500">✕</button>
          {children}
        </div>
      </div>
    </>
  );
};

export default ModalBase;
