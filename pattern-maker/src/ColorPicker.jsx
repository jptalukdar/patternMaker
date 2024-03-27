

function ReactColourPicker() {
  const [color, setColor] = useState("#000000");

  return (
    <div>
      <input
        type="color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
      />
      <p>{color}</p>
    </div>
  );
}