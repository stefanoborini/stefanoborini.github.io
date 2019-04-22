---
category: fortran
title: Reference counting in Fortran 95 (incomplete)
---
# Reference counting in Fortran 95

Here is a problem which is not only found in Fortran, but in all non
memory-managed languages: who is in charge of deleting an object? All this
stuff can be handled in C++ with plenty of off-the-shelf features, such as
destructors and some STL/Boost classes, but nothing exists like that exists 
for Fortran. We will have to reinvent the wheel.

One option, and the one I stuck with for a while, was to bless object e.g.
``Car`` with the magic duty to delete its dependent object ``Engine``. That
means, ``Car`` owns ``Engine``, and the life of ``Engine`` depends on the life
of ``Car``. If ``Car`` is deleted, ``Engine`` is deleted. If another object
``EngineList`` is interested in ``Engine``, we have three choices

- ``EngineList`` gets a pointer to ``Engine`` from ``Car`` and stores it, or
- ``EngineList`` steals the responsibility from ``Car`` to delete ``Engine``,
  that is, ownership is transferred from ``Car`` to ``EngineList`` or
- ``EngineList`` gets a copy of ``Engine``, and is now responsible of managing the life of the copy.
- ``EngineList``, ``Car`` and ``Engine`` collaborate in a reference counting mechanism.
  Either ``EngineList`` or ``Car`` can issue a "deletion request" but only when
  no object is left referencing ``Engine``, this will be deleted.

This is a trivial example of course, and depending on the actual names and
roles of the types involved, one solution may be better and more intuitive than
another. Keep this example as a general guide,

With the first solution, if you delete ``Car`` later in your code, ``Engine``
is also deleted. This makes the pointer in ``EngineList`` invalid. Using this
pointer will lead to a crash. To prevent this, you have to plan for a proper
allocation strategy: all objects always store a pointer and never own
the object, and delegate the responsibility for deletion (and therefore lifetime)
to someone else. For example, you may have an ``Application`` object who owns
the ``Engine`` and therefore the responsibility of deleting it, guaranteeing a
proper lifetime for all your entities. ``Application`` then creates ``Car`` and
sets the ``Engine``, so that ``Engine`` survives until ``Application``
survives. This is apparently a fair solution, but it makes ``Application``
aware of a problem and in charge of a responsibility which is there just
because of technical problem, not because it has a real domain need to know
about these details.

The second solution, transferring ownership, leaves a ``Car`` without the
``Engine``. I generally relied on this solution because it generally worked ok,
but for this specific example is probably not the best choice. In any case, the
main idea is to move the responsibility for deletion from one object to
another. I generally handled one-to-one interest: only one object A was
interested in another object B. When a new object C was interested in B, A also
lost interest in it, and it made sense within that context. To do this, I
implemented two methods on the objects: ``Relinquish`` and ``Grab``. In our
example it would be

```fortran
    module EngineModule
       implicit none
       private

       public :: EngineType
       public :: new, delete

       type EngineType
           integer :: horsePower
       end type

      interface new
          module procedure newImpl
      end interface
      interface delete
          module procedure deleteImpl
      end interface

    contains
        subroutine newImpl(self, horsePower)
            type (EngineType), intent(inout) :: self
            integer, intent(in) :: horsePower
     
            self%horsePower = horsePower
        end subroutine
        subroutine deleteImpl(self)
            type (EngineType), intent(inout) :: self
            ! nothing to do. 
        end subroutine

    end module
```

This is the Car

```fortran
    module CarModule
       use EngineModule
       implicit none
       private

       public :: CarType
       public :: new, delete, relinquishEngine

       type CarType
           type(EngineType), pointer :: engine => null()
       end type

      interface new
          module procedure newImpl
      end interface
      interface delete
          module procedure deleteImpl
      end interface

    contains
        subroutine newImpl(self)
            type (CarType), intent(inout) :: self
     
            if (associated(self%engine)) then
                  ! handle error, double instantiation
            endif

            allocate(self%engine)
            call New(self%engine, 40)
        end subroutine

        subroutine deleteImpl(self)
            type (CarType), intent(inout) :: self

            if (associated(self%engine)) then
                 call Delete(self%engine)
                 deallocate(self%engine)
                 nullify(self%engine)
            endif
        end subroutine

        function relinquishEngine(self) result(enginePtr)
            type (CarType), intent(inout) :: self
            type (EngineType), pointer :: enginePtr

            enginePtr => self%engine ! give it out
            nullify(self%engine) ! no longer the owner
        end subroutine

    end module
```

Note how the ``deleteImpl`` routine deletes the engine member only if the pointer is associated, and
how the relinquish function returns the pointer and nullifies the current member. This is the first
part of ownership transfer. The second part is in ownership acquisition in the ``EngineList`` grab routine

```fortran
    subroutine grabEngine(self, enginePtr)
       ! takes ownership of an engine object (which has been relinquished by someone else)
       type(EngineListType), intent(inout) :: self
       type(EngineType), pointer :: enginePtr

       self%engine => enginePtr
    end subroutine
```

With reference counting:

```fortran
module RefCount
    implicit none

    type ObjectType
        integer :: refCount = 0
        integer, pointer :: data(:)
    end type

    type ObjectRefType
        type (ObjectType), pointer :: object => null()
    end type
    interface New
        module procedure NewObject
    end interface
    interface Ref
        module procedure NewRefFromObject
        module procedure NewRefFromRef
    end interface
    interface Delete
        module procedure DeleteObject
        module procedure DeleteRef
    end interface
    interface Deref
        module procedure DerefPrivate
    end interface

contains

    subroutine NewObject(self)
        type (ObjectType), intent(inout)  :: self

        print *, "New Object"
        allocate(self%data(10))
        self%data = 1.0
        self%RefCount = 0

    end subroutine
    subroutine DeleteObject(self)
        type (ObjectType), intent(inout)  :: self

        if (self%refCount /= 0) print *, "refcount .not. zero. Big mistake!"

        print *, "Deleting object"
        deallocate(self%data)

    end subroutine

    function NewRefFromObject(object) result(ref)
        type (ObjectType), pointer :: object
        type (ObjectRefType), pointer :: Ref

        allocate(Ref)
        Ref%object => object
        Ref%object%refCount = Ref%object%refCount + 1
        print *, "New reference. Count = ", Ref%object%refCount
    end function
    function NewRefFromRef(ref) result(newref)
        type (ObjectRefType), pointer :: ref
        type (ObjectRefType), pointer :: newref

        allocate(NewRef)
        NewRef%object => ref%object
        NewRef%object%refCount = NewRef%object%refCount + 1
        print *, "New reference. Count = ", NewRef%object%refCount
    end function
    subroutine DeleteRef(ref)
        type (ObjectRefType), pointer :: ref

        ref%object%refCount = ref%object%refCount - 1
        if (ref%object%refCount == 0) then
            print *, "Deleting object. Reference count dropped to zero"
            call Delete(ref%object)
            deallocate(ref%object)
            deallocate(ref)
            return
        endif

        print *, "Unreferencing. Reference count dropped to ",ref%object%refCount
    end subroutine
    function DerefPrivate(ref)
        type (ObjectRefType), pointer :: ref
        type (ObjectType), pointer :: DerefPrivate

        DerefPrivate => ref%object
    end function

end module

program m
    use RefCount
    type (ObjectType), pointer :: object, objectPtr
    type (ObjectRefType), pointer :: ref1, ref2, ref3

    allocate(object)
    call New(object)

    object%data = 10.0

    ref1 => Ref(object)
    ref2 => Ref(object)
    ref3 => Ref(ref1)

    objectPtr => deRef(ref3)
    objectPtr%data = 2.0

    objectPtr => deRef(ref2)

    print *, objectPtr%data

    call Delete(ref1)
    call Delete(ref2)
    call Delete(ref3)
end
```
