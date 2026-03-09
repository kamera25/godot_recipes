

フローチャートを使用した具体例

もし任意の関数がこのイベントを処理する場合、Viewport.set_input_as_handled() を呼び出すことで、そのイベントがこれ以上伝播しないようにできます。

If the control wants to "consume" the event, it will call Control.accept_event() and the event will not spread any more
