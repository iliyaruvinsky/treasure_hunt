import React, { useState, useRef, useEffect } from 'react';

interface HelpTooltipProps {
  content: string | React.ReactNode;
  title?: string;
}

const HelpTooltip: React.FC<HelpTooltipProps> = ({ content, title }) => {
  const [show, setShow] = useState(false);
  const [position, setPosition] = useState<'bottom' | 'top'>('bottom');
  const tooltipRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (show && tooltipRef.current && buttonRef.current) {
      // Use setTimeout to ensure tooltip is rendered before checking position
      setTimeout(() => {
        if (tooltipRef.current && buttonRef.current) {
          const tooltip = tooltipRef.current;
          const button = buttonRef.current;
          const tooltipRect = tooltip.getBoundingClientRect();
          const buttonRect = button.getBoundingClientRect();
          
          // Check if tooltip would be cut off at top (less than 10px from top of viewport)
          if (buttonRect.top - tooltipRect.height < 10) {
            setPosition('bottom');
          } else {
            setPosition('top');
          }
        }
      }, 0);
    }
  }, [show]);

  return (
    <span className="position-relative d-inline-block ms-2">
      <button
        ref={buttonRef}
        type="button"
        className="btn btn-link p-0 border-0 text-white"
        style={{ fontSize: '0.9rem', lineHeight: '1', textDecoration: 'none' }}
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        onClick={() => setShow(!show)}
        aria-label="Help"
      >
        <i className="bi bi-question-circle" style={{ fontSize: '1.1rem' }}></i>
      </button>
      {show && (
        <div
          ref={tooltipRef}
          className="position-absolute bg-dark text-white p-3 rounded shadow-lg"
          style={{
            zIndex: 1000,
            minWidth: '300px',
            maxWidth: '400px',
            ...(position === 'top' 
              ? {
                  bottom: '100%',
                  marginBottom: '8px',
                }
              : {
                  top: '100%',
                  marginTop: '8px',
                }
            ),
            left: '50%',
            transform: 'translateX(-50%)',
            fontSize: '0.9rem',
            lineHeight: '1.5',
          }}
          onMouseEnter={() => setShow(true)}
          onMouseLeave={() => setShow(false)}
        >
          {title && <strong className="d-block mb-2">{title}</strong>}
          <div>{content}</div>
          <div
            className="position-absolute"
            style={{
              ...(position === 'top'
                ? {
                    bottom: '-5px',
                    borderLeft: '5px solid transparent',
                    borderRight: '5px solid transparent',
                    borderTop: '5px solid #212529',
                  }
                : {
                    top: '-5px',
                    borderLeft: '5px solid transparent',
                    borderRight: '5px solid transparent',
                    borderBottom: '5px solid #212529',
                  }
              ),
              left: '50%',
              transform: 'translateX(-50%)',
              width: 0,
              height: 0,
            }}
          ></div>
        </div>
      )}
    </span>
  );
};

export default HelpTooltip;

