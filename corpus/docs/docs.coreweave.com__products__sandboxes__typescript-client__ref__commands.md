# Commands and terminals

Source: https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands

# Commands and terminals

> TypeScript declarations for commands and terminals in @coreweave/cwsandbox 1.0.0.

API reference for `@coreweave/cwsandbox` version **1.0.0**. For installation and authentication, see the [TypeScript client guide](https://docs.coreweave.com/products/sandboxes/typescript-client.md).

Declarations, including parameter types, return types, overloads, and comments, come from the [published package](https://www.npmjs.com/package/@coreweave/cwsandbox/v/1.0.0). An optional member has a `?` suffix. Inherited members are defined on the linked parent type.

## Command

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { Command } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type Command = readonly [
    string,
    ...string[]
];
```

## CommandInput

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandInput } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type CommandInput = Command | ReadonlyArray<string>;
```

Related types: [`Command`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#command).

## CommandInputData

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandInputData } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type CommandInputData = string | Uint8Array;
```

## CommandInputWriter

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandInputWriter } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface CommandInputWriter {
    readonly closed: boolean;
    close(options?: RequestOptions): Promise<void>;
    write(data: CommandInputData, options?: RequestOptions): Promise<void>;
    writeln(text: string, options?: RequestOptions): Promise<void>;
}
```

Related types: [`CommandInputData`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinputdata), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## CommandOutputStream

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandOutputStream } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type CommandOutputStream = AsyncIterable<string>;
```

## CommandProcess

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandProcess } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface CommandProcess {
    readonly command: Command;
    readonly exitCode: number | undefined;
    readonly stderr: CommandOutputStream;
    readonly status: CommandProcessStatus;
    readonly stdout: CommandOutputStream;
    cancel(options?: RequestOptions): Promise<void>;
    poll(): number | undefined;
    wait(options?: RequestOptions): Promise<ProcessResult>;
}
```

Related types: [`Command`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#command), [`CommandOutputStream`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandoutputstream), [`CommandProcessStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandprocessstatus), [`ProcessResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#processresult), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## CommandProcessStatus

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandProcessStatus } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
type CommandProcessStatus = "cancelled" | "exited" | "failed" | "running" | "starting";
```

## CommandProcessWithStdin

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { CommandProcessWithStdin } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface CommandProcessWithStdin extends CommandProcess {
    readonly stdin: CommandInputWriter;
}
```

Related types: [`CommandInputWriter`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinputwriter), [`CommandProcess`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandprocess).

## ExecOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ExecOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ExecOptions extends RequestOptions {
    readonly check?: boolean;
    readonly cwd?: string;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## ProcessResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ProcessResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ProcessResult {
    readonly command: Command;
    readonly exitCode: number;
    readonly failed: boolean;
    readonly ok: boolean;
    readonly stderr: string;
    readonly stderrBytes: Uint8Array;
    readonly stderrBytesProduced: number;
    readonly stderrTruncated: boolean;
    readonly stdout: string;
    readonly stdoutBytes: Uint8Array;
    readonly stdoutBytesProduced: number;
    readonly stdoutTruncated: boolean;
}
```

Related types: [`Command`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#command).

## SandboxCommands

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { SandboxCommands } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface SandboxCommands {
    run(command: CommandInput, options?: ExecOptions): Promise<ProcessResult>;
    start(command: CommandInput, options: StartCommandOptionsWithStdin): Promise<CommandProcessWithStdin>;
    start(command: CommandInput, options?: StartCommandOptions): Promise<CommandProcess>;
}
```

Related types: [`CommandInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinput), [`CommandProcess`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandprocess), [`CommandProcessWithStdin`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandprocesswithstdin), [`ExecOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#execoptions), [`ProcessResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#processresult), [`StartCommandOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#startcommandoptions), [`StartCommandOptionsWithStdin`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#startcommandoptionswithstdin).

## ShellOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { ShellOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface ShellOptions extends RequestOptions {
    readonly cols?: number;
    readonly command?: CommandInput;
    readonly rows?: number;
}
```

Related types: [`CommandInput`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinput), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## StartCommandOptions

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { StartCommandOptions } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface StartCommandOptions extends RequestOptions {
    readonly bufferedMaxKiB?: number;
    readonly check?: boolean;
    readonly cwd?: string;
    readonly stdin?: boolean;
}
```

Related types: [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions).

## StartCommandOptionsWithStdin

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { StartCommandOptionsWithStdin } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface StartCommandOptionsWithStdin extends StartCommandOptions {
    readonly stdin: true;
}
```

Related types: [`StartCommandOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#startcommandoptions).

## TerminalResult

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { TerminalResult } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface TerminalResult {
    readonly command: Command;
    readonly exitCode: number;
}
```

Related types: [`Command`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#command).

## TerminalSession

[Published declaration](https://unpkg.com/@coreweave/cwsandbox@1.0.0/dist/client-DpqdEOsC.d.ts).

```typescript theme={"system"}
import type { TerminalSession } from "@coreweave/cwsandbox";
```

```typescript theme={"system"}
interface TerminalSession {
    readonly command: Command;
    readonly exitCode: number | undefined;
    readonly output: AsyncIterable<Uint8Array>;
    readonly stdin: CommandInputWriter;
    readonly status: CommandProcessStatus;
    cancel(options?: RequestOptions): Promise<void>;
    poll(): number | undefined;
    resize(cols: number, rows: number, options?: RequestOptions): Promise<void>;
    wait(options?: RequestOptions): Promise<TerminalResult>;
}
```

Related types: [`Command`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#command), [`CommandInputWriter`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandinputwriter), [`CommandProcessStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#commandprocessstatus), [`RequestOptions`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/common#requestoptions), [`TerminalResult`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/commands#terminalresult).
