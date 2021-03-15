import { environment } from 'src/environments/environment';


export class Log {

    public static l(tag: any = '', message: any = '') {
        if (environment.production)
            return;
        console.log('[L]', tag, message);
    }

    public static i(tag: any = '', message: any = '') {
        if (environment.production)
            return;
        console.info('[I]', tag, message);
    }

    public static d(tag: any = '', message: any = '') {
        if (environment.production)
            return;
        console.debug('[D]', tag, message);
    }

    public static e(tag: any = '', message: any = '') {
        if (environment.production)
            return;
        console.error('[E]', tag, message);
    }

    public static w(tag: any, message: any = '') {
        if (environment.production)
            return;
        console.warn('[W]', tag, message);
    }

    public static t(tag: any = '', message: any = '') {
        if (environment.production)
            return;
        console.trace('[T]', tag, message);
    }

}