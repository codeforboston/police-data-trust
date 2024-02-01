// pages/index.tsx

import { useState } from 'react';

const ToggleForm = () => {
  const [selectedOption, setSelectedOption] = useState<string>('Option 1');
  const options = ['Option 1', 'Option 2', 'Option 3'];

  const handleToggleChange = (option: string) => {
    setSelectedOption(option);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Perform form submission with selectedOption
    console.log('Form submitted with selected option:', selectedOption);
    // Add logic to handle form submission (e.g., send data to a server)
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Select an option:</label>
        {options.map((option) => (
          <div key={option}>
            <input
              type="radio"
              id={option}
              name="toggleOptions"
              value={option}
              checked={selectedOption === option}
              onChange={() => handleToggleChange(option)}
            />
            <label htmlFor={option}>{option}</label>
          </div>
        ))}
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default ToggleForm;
eter