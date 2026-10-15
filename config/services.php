<?php

declare(strict_types=1);

use Symfony\Component\DependencyInjection\Loader\Configurator\ContainerConfigurator;
use Xormania\Uxorscient\Mate\Companion;
use Xormania\Uxorscient\NativeTools;
use Xormania\Uxorscient\Operations;
use Xormania\Uxorscient\ProjectDoctor;
use Xormania\Uxorscient\ProjectInspector;
use Xormania\Uxorscient\ReferenceBundle;

return static function (ContainerConfigurator $container): void {
    $services = $container->services();
    foreach ([ReferenceBundle::class, ProjectInspector::class, ProjectDoctor::class, NativeTools::class, Operations::class] as $class) {
        $services->set($class)->autowire();
    }
    $services->set(Companion::class)->autowire()->arg('$projectRoot', '%mate.root_dir%');
};
