# Bad React
There are pretty strict React rules/guidelines that can be unintuitive. Here's a list of React paradigms to avoid that I've found while working at TACC.

### When do we re-render?
It's a common misconception that React will re-render a component when that component's props change. **Components do NOT re-render when props change!** The render process doesn't care what a component's props are. React's default behavior is to re-render components when *that component's parent* re-renders, usually through a `setState()` call.

The only time changing props matters is if you're using `React.useMemo()`.

### Nested Component Types
You must never **create new component types while rendering!** React's rendering logic will first compare elements based on their `type`. If an element's `type` changes (like going from a `<div>` to a `<span>` or from `<ComponentA>` to `<ComponentB>`), React will assume that the entire tree below that element has changed.
Whenever you create a new component type, it's a different reference. This will cause React to repeatedly destroy and recreate the child component tree!
```jsx
// BAD! this creates a new 'ChildComponent' reference every time!
const ParentComponent = () => {
	const ChildComponent = () => {
		return (<div>Hi</div>);
	};

	return (<ChildComponent />);
};
```
Instead, always define components *separately*:
```jsx
// GOOD! this creates only one component type reference
const ChildComponent = () => {
	return (<div>Hi</div>);
}

const ParentComponent = () => {
	return (<ChildComponent />);
}
```

### Keys in Lists
React will ask for a `key` prop when mapping over an array and rendering each element. It's bad form to use `key={index}` in your rendering; it's better to use a unique ID that comes from the data. (in our pansim project, we map over each county object to display in the right-side table. I changed the `key` from `index` to `county.fips`).
Consider we render a list of 10 `<TodoListItem>` components using array indices as keys:
```jsx
// Bad keys, shitty rendering
todos.map((todo, index) => <TodoListItem key={index} todo={todo} />);
```
React sees 10 items with keys `0..9`. If we delete items 6 and 7, and add three new entries at the end, we end up rendering items with keys `0..10`. To React, it looks like I just added one new entry to the end! React will reuse the existing DOM nodes and component instances, but we're probably now rendering `<TodoListItem key={6}>` with the todo item that *was* passed to list item 8. The component instance is still alive, but is now getting different data than is was previously. This can lead to unexpected behavior!
React now also has to go apply updates to several of the list items to change the text and other DOM contents because the existing list items now have to show different data. These updates are unnecessary since none of the list items have actually changed.

If we use a unique ID for each item, React will correctly see that we deleted two items and added three new ones. It destroys the two deleted components (and their associated DOM nodes) and create three new component instances (and their DOM nodes). The components whose data was unchanged are no longer updated!
```jsx
// Good keys! Better rendering!
todos.map((todo) => <TodoListItem key={todo.id} todo={todo} />);
```
